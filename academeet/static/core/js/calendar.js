class Calendar {
    constructor() {
        this.date = new Date();
        this.holidays = {};
        this.tooltipElement = document.getElementById('holidayTooltip');
        this.holidayListElement = document.getElementById('holidayDetailsList');
        this.init();
    }

    async init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.setupEventListeners();
                this.loadHolidays().then(() => this.render());
            });
        } else {
            this.setupEventListeners();
            await this.loadHolidays();
            this.render();
        }
    }

    setupEventListeners() {
        const prevButton = document.getElementById('prevMonth');
        const nextButton = document.getElementById('nextMonth');

        if (prevButton && nextButton) {
            prevButton.addEventListener('click', () => {
                this.date.setMonth(this.date.getMonth() - 1);
                this.loadHolidays().then(() => this.render());
            });

            nextButton.addEventListener('click', () => {
                this.date.setMonth(this.date.getMonth() + 1);
                this.loadHolidays().then(() => this.render());
            });
        }

        // Handle tooltip positioning
        document.addEventListener('mousemove', (e) => {
            const target = e.target;
            if (target && target.classList && target.classList.contains('holiday')) {
                const rect = target.getBoundingClientRect();
                const holidayObj = this.holidays[target.dataset.date];
                if (holidayObj) {
                    // Pass an object with date and name so showTooltip can format
                    this.showTooltip({ date: target.dataset.date, name: holidayObj.name }, rect);
                }
            } else {
                this.hideTooltip();
            }
        });
    }

    async loadHolidays() {
        const year = this.date.getFullYear();
        const month = this.date.getMonth() + 1;
        let data = [];
        try {
            const response = await fetch(`/api/holidays/${year}/${month}/`);
            data = await response.json();
        } catch (error) {
            console.error('Error loading holidays:', error);
        }

        // Always add recurring national holidays if not present
        const recurringNational = [
            { month: 1, day: 1, name: "New Year's Day" },
            { month: 1, day: 23, name: "First Philippine Republic Day" },
            { month: 1, day: 29, name: "Chinese New Year" },
            { month: 2, day: 2, name: "Constitution Day" },
            { month: 2, day: 12, name: "Lantern Festival" },
            { month: 2, day: 25, name: "EDSA Revolution Anniversary" },
            { month: 3, day: 30, name: "End of Ramadan (Eid al-Fitr)" },
            { month: 4, day: 9, name: "Day of Valor" },
            { month: 4, day: 17, name: "Maundy Thursday" },
            { month: 4, day: 18, name: "Good Friday" },
            { month: 4, day: 19, name: "Easter Saturday" },
            { month: 4, day: 20, name: "Easter Sunday" },
            { month: 4, day: 27, name: "Lapu-Lapu Day" },
            { month: 5, day: 1, name: "Labour Day" },
            { month: 6, day: 6, name: "Feast of the Sacrifice (Eid al-Adha)" },
            { month: 6, day: 12, name: "Independence Day" },
            { month: 6, day: 19, name: "José Rizal's birthday" },
            { month: 6, day: 26, name: "Islamic New Year" },
            { month: 7, day: 27, name: "Iglesia ni Cristo Day" },
            { month: 8, day: 21, name: "Ninoy Aquino Day" },
            { month: 8, day: 25, name: "National Heroes' Day" },
            { month: 9, day: 4, name: "Birthday of Muhammad (Mawlid)" },
            { month: 10, day: 6, name: "Mid-Autumn Festival" },
            { month: 11, day: 1, name: "All Saints' Day" },
            { month: 11, day: 2, name: "All Souls' Day" },
            { month: 11, day: 30, name: "Bonifacio Day" },
            { month: 12, day: 8, name: "Feast of the Immaculate Conception of the Blessed Virgin" },
            { month: 12, day: 24, name: "Christmas Eve" },
            { month: 12, day: 25, name: "Christmas Day" },
            { month: 12, day: 30, name: "Rizal Day" },
            { month: 12, day: 31, name: "New Year's Eve" }
        ];

        // Only add if not already present in data
        const datesInData = new Set(data.map(h => h.date));
        recurringNational.forEach(h => {
            const dateStr = `${year}-${String(h.month).padStart(2, '0')}-${String(h.day).padStart(2, '0')}`;
            if (!datesInData.has(dateStr) && month === h.month) {
                data.push({ date: dateStr, name: h.name, school_specific: false });
            }
        });

        // Normalize holiday objects so we can show date + name in tooltip
        this.holidays = data.reduce((acc, holiday) => {
            const name = holiday.holiday_name || holiday.name || holiday.holiday || holiday.title || '';
            acc[holiday.date] = { name, raw: holiday };
            return acc;
        }, {});
    }

    showTooltip(text, targetRect) {
        // allow passing either string or object { date, name }
        const textToShow = typeof text === 'string' ? text : (text.name ? `${text.date} — ${text.name}` : JSON.stringify(text));
        this.tooltipElement.textContent = textToShow;
        this.tooltipElement.classList.add('visible');

        // Position the tooltip above the date
        const tooltipRect = this.tooltipElement.getBoundingClientRect();
        const top = targetRect.top - tooltipRect.height - 10;
        const left = targetRect.left + (targetRect.width / 2) - (tooltipRect.width / 2);

        this.tooltipElement.style.top = `${top}px`;
        this.tooltipElement.style.left = `${left}px`;
    }

    hideTooltip() {
        this.tooltipElement.classList.remove('visible');
    }

    updateHolidaysList() {
        if (!this.holidayListElement) return;

        // Separate holidays by type
        const holidays = Object.entries(this.holidays).map(([dateStr, holidayObj]) => ({
            date: dateStr,
            name: holidayObj.name,
            formattedDate: this.formatDateForDisplay(dateStr),
            schoolSpecific: holidayObj.raw && holidayObj.raw.school_specific
        })).sort((a, b) => a.date.localeCompare(b.date));

        const national = holidays.filter(h => !h.schoolSpecific);
        const school = holidays.filter(h => h.schoolSpecific);

        let html = '';

        // National Holidays Section
        html += `<h4 style="color: #B30000; margin-bottom: 0.5rem; text-align: left;">🎉 National Holidays</h4>`;
        if (national.length === 0) {
            html += '<li style="color: #999;">No national holidays this month</li>';
        } else {
            html += national.map(holiday =>
                `<li><span style="color: #AC0000; font-weight: 600;">${holiday.formattedDate}</span> – ${holiday.name}</li>`
            ).join('');
        }

        // School-Specific Holidays Section
        html += `<h4 style="color: #B8860B; margin: 1.2em 0 0.3em 0; text-align: left;">⭐ School-Declared Dates</h4>`;
        html += `<div class="school-holiday-explanation" style="color: #B8860B; font-size: 0.95em; margin-bottom: 0.5em;">
            ⭐ School-Declared Dates are special holidays or events set by the school administration. These dates may include foundation days, school fairs, or other important events unique to the institution. Only school administrators can add, edit, or remove these dates.
        </div>`;
        if (school.length === 0) {
            html += '<li style="color: #999;">No school-declared dates this month</li>';
        } else {
            html += school.map(holiday =>
                `<li><span class="gold-marker" style="color: #FFD700; font-weight: bold; margin-right: 0.3em;">⭐</span><span style="color: #B8860B; font-weight: 600;">${holiday.formattedDate}</span> – ${holiday.name}</li>`
            ).join('');
        }

        this.holidayListElement.innerHTML = html;
    }

    formatDateForDisplay(dateStr) {
        // Convert YYYY-MM-DD to "Month DD"
        const date = new Date(dateStr + 'T00:00:00Z');
        return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric' });
    }

    render() {
        // Update month/year display
        const monthYearText = this.date.toLocaleString('default', { 
            month: 'long', 
            year: 'numeric' 
        });
        document.getElementById('monthYear').textContent = monthYearText;

        const tbody = document.getElementById('calendarBody');
        tbody.innerHTML = '';

        // Get first day of month and total days
        const firstDay = new Date(this.date.getFullYear(), this.date.getMonth(), 1);
        const lastDay = new Date(this.date.getFullYear(), this.date.getMonth() + 1, 0);
        
        let currentDay = 1;
        const today = new Date();

        // Create calendar grid
        for (let i = 0; i < 6; i++) {
            const row = document.createElement('tr');
            
            for (let j = 0; j < 7; j++) {
                const cell = document.createElement('td');
                
                if (i === 0 && j < firstDay.getDay()) {
                    cell.textContent = '';
                } else if (currentDay > lastDay.getDate()) {
                    cell.textContent = '';
                } else {
                    cell.textContent = currentDay;
                    
                    // Format date string for holiday lookup
                    const dateStr = `${this.date.getFullYear()}-${String(this.date.getMonth() + 1).padStart(2, '0')}-${String(currentDay).padStart(2, '0')}`;
                    
                    // Check if current date is a holiday
                    if (this.holidays[dateStr]) {
                        cell.classList.add('holiday');
                        cell.dataset.date = dateStr;
                    }
                    
                    // Highlight current day
                    if (this.date.getFullYear() === today.getFullYear() &&
                        this.date.getMonth() === today.getMonth() &&
                        currentDay === today.getDate()) {
                        cell.classList.add('current-day');
                    }
                    
                    currentDay++;
                }
                
                row.appendChild(cell);
            }
            
            tbody.appendChild(row);
            if (currentDay > lastDay.getDate()) break;
        }

        // Update the holiday details list
        this.updateHolidaysList();
    }
};

// Initialize calendar when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Calendar();
});