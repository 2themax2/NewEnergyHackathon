// src/app/services/data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, timer } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';

// Define interfaces for our data structures
export interface EnergyMetric {
  id: string;
  title: string;
  value: number;
  unit: string;
  trend: 'up' | 'down' | 'stable';
  iconClass?: string; // e.g., 'fas fa-bolt'
  lastUpdated: string;
  details?: string; // Optional additional details
  chartData?: {
    labels: string[];
    values: number[];
  };
}

export interface DashboardData {
  summary: {
    totalConsumption: EnergyMetric;
    renewableGeneration: EnergyMetric;
    gridImport: EnergyMetric;
    carbonFootprint: EnergyMetric;
  };
  detailedMetrics: EnergyMetric[];
}

@Injectable({
  providedIn: 'root'
})
export class DataService {
  // In a real app, this would be your API endpoint
  // private apiUrl = 'http://localhost:3000/api/energy-data'; // Example API URL

  constructor(private http: HttpClient) { }

  // Simulate fetching data with a delay and random updates
  getDashboardData(): Observable<DashboardData> {
    // Use 'of' for dummy data, or 'this.http.get<DashboardData>(this.apiUrl)' for a real API
    return timer(500, 15000) // Emit initial value after 500ms, then update every 15 seconds
      .pipe(
        switchMap(() => of(this.generateDummyData()))
      );
  }

  private generateDummyData(): DashboardData {
    const now = new Date();
    const randomFactor = (min: number, max: number) => Math.random() * (max - min) + min;
    const randomInt = (min: number, max: number) => Math.floor(randomFactor(min, max));

    const generateChartData = (baseValue: number, points: number = 7) => {
      const labels = Array.from({length: points}, (_, i) => `Day ${i + 1}`);
      const values = Array.from({length: points}, () => baseValue + randomInt(-baseValue * 0.2, baseValue * 0.2));
      return { labels, values };
    };

    return {
      summary: {
        totalConsumption: {
          id: 'total-consumption',
          title: 'Total Consumption',
          value: parseFloat(randomFactor(1500, 2500).toFixed(2)),
          unit: 'kWh',
          trend: Math.random() > 0.5 ? 'up' : 'down',
          iconClass: 'fas fa-bolt',
          lastUpdated: now.toLocaleTimeString(),
          chartData: generateChartData(2000)
        },
        renewableGeneration: {
          id: 'renewable-generation',
          title: 'Renewable Generation',
          value: parseFloat(randomFactor(800, 1200).toFixed(2)),
          unit: 'kWh',
          trend: 'up',
          iconClass: 'fas fa-solar-panel',
          lastUpdated: now.toLocaleTimeString(),
          chartData: generateChartData(1000)
        },
        gridImport: {
          id: 'grid-import',
          title: 'Grid Import',
          value: parseFloat(randomFactor(700, 1300).toFixed(2)),
          unit: 'kWh',
          trend: Math.random() > 0.3 ? 'stable' : 'down',
          iconClass: 'fas fa-plug-circle-bolt',
          lastUpdated: now.toLocaleTimeString(),
        },
        carbonFootprint: {
          id: 'carbon-footprint',
          title: 'Carbon Footprint',
          value: parseFloat(randomFactor(300, 500).toFixed(2)),
          unit: 'kg CO2e',
          trend: 'down',
          iconClass: 'fas fa-leaf',
          lastUpdated: now.toLocaleTimeString(),
        }
      },
      detailedMetrics: [
        {
          id: 'peak-demand',
          title: 'Peak Demand Today',
          value: parseFloat(randomFactor(5, 15).toFixed(2)),
          unit: 'kW',
          trend: 'stable',
          iconClass: 'fas fa-tachometer-alt-fast',
          lastUpdated: now.toLocaleTimeString(),
          details: `Occurred at ${randomInt(0,23).toString().padStart(2,'0')}:${randomInt(0,59).toString().padStart(2,'0')}`
        },
        {
          id: 'energy-cost',
          title: 'Estimated Cost',
          value: parseFloat(randomFactor(50, 150).toFixed(2)),
          unit: 'USD',
          trend: 'up',
          iconClass: 'fas fa-dollar-sign',
          lastUpdated: now.toLocaleTimeString(),
          details: 'Based on current tariff'
        },
        {
          id: 'battery-storage',
          title: 'Battery Storage',
          value: randomInt(20, 90),
          unit: '%',
          trend: Math.random() > 0.6 ? 'up' : 'down',
          iconClass: 'fas fa-car-battery',
          lastUpdated: now.toLocaleTimeString(),
          chartData: { labels: ['1h ago', '30m ago', 'Now'], values: [randomInt(20,90), randomInt(20,90), randomInt(20,90)] }
        },
        {
          id: 'solar-efficiency',
          title: 'Solar Panel Efficiency',
          value: parseFloat(randomFactor(15, 22).toFixed(1)),
          unit: '%',
          trend: 'stable',
          iconClass: 'fas fa-sun',
          lastUpdated: now.toLocaleTimeString(),
          details: 'Current output vs. max capacity'
        }
      ]
    };
  }
}
