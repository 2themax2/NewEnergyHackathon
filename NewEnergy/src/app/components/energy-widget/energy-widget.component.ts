// src/app/components/energy-widget/energy-widget.component.ts
import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EnergyMetric } from '../../services/data.service'; // Import the interface

// Chart.js for simple charts (optional, but adds a nice touch)
// You'd need to install chart.js: npm install chart.js
// And then import it. For simplicity, I'll keep the chart logic minimal here.
// If you use Chart.js, you might want to make a dedicated chart component.
// import { Chart, registerables } from 'chart.js';
// Chart.register(...registerables);


@Component({
  selector: 'app-energy-widget',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './energy-widget.component.html',
  styleUrls: ['./energy-widget.component.css']
})
export class EnergyWidgetComponent implements OnInit, OnChanges {
  @Input() metric!: EnergyMetric; // Input property to pass data to the widget
  @Input() widgetType: 'summary' | 'detail' = 'detail'; // To vary styling slightly

  previousValue: number | null = null;
  valueChangeIndicator: 'increased' | 'decreased' | 'none' = 'none';

  constructor() {}

  ngOnInit(): void {
    if (this.metric) {
      this.previousValue = this.metric.value; // Initialize previous value
    }
    // If using Chart.js, initialize chart here if metric.chartData exists
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['metric'] && !changes['metric'].firstChange) {
      const currentValue = changes['metric'].currentValue.value;
      const previousValue = changes['metric'].previousValue?.value;

      if (previousValue !== null && currentValue !== previousValue) {
        this.valueChangeIndicator = currentValue > previousValue ? 'increased' : 'decreased';
        // Reset indicator after a short delay
        setTimeout(() => this.valueChangeIndicator = 'none', 1500);
      }
      this.previousValue = currentValue;
      // If using Chart.js, update chart here
    }
  }

  getTrendIcon(): string {
    if (this.metric.trend === 'up') return 'fas fa-arrow-trend-up text-success';
    if (this.metric.trend === 'down') return 'fas fa-arrow-trend-down text-danger';
    return 'fas fa-minus text-warning'; // For 'stable'
  }

  getTrendColorClass(): string {
    if (this.metric.trend === 'up') return 'trend-up';
    if (this.metric.trend === 'down') return 'trend-down';
    return 'trend-stable';
  }

  getValueChangeClass(): string {
    if (this.valueChangeIndicator === 'increased') return 'value-increased';
    if (this.valueChangeIndicator === 'decreased') return 'value-decreased';
    return '';
  }
}
