// src/app/pages/dashboard/dashboard.component.ts
import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription, Observable } from 'rxjs';
import { DataService, DashboardData, EnergyMetric } from '../../services/data.service';
import { EnergyWidgetComponent } from '../../components/energy-widget/energy-widget.component'; // Import the widget

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, EnergyWidgetComponent], // Add EnergyWidgetComponent
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, OnDestroy {
  dashboardData$: Observable<DashboardData | null>;
  isLoading: boolean = true;
  error: string | null = null;

  // For direct access if needed, though async pipe is preferred
  // currentDashboardData: DashboardData | null = null;
  // private dataSubscription!: Subscription;

  constructor(private dataService: DataService) {
    this.dashboardData$ = this.dataService.getDashboardData();
  }

  ngOnInit(): void {
    // The async pipe handles subscription and unsubscription automatically.
    // If you were to subscribe manually:
    /*
    this.isLoading = true;
    this.dataSubscription = this.dataService.getDashboardData().subscribe({
      next: (data) => {
        this.currentDashboardData = data;
        this.isLoading = false;
        this.error = null;
      },
      error: (err) => {
        console.error('Error fetching dashboard data:', err);
        this.error = 'Failed to load energy data. Please try again later.';
        this.isLoading = false;
      }
    });
    */
  }

  ngOnDestroy(): void {
    // Unsubscribe if manually subscribed to prevent memory leaks
    // if (this.dataSubscription) {
    //   this.dataSubscription.unsubscribe();
    // }
  }

  // Helper to track items in *ngFor for better performance
  trackByMetricId(index: number, metric: EnergyMetric): string {
    return metric.id;
  }
}
