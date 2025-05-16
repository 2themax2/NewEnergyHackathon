// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard.component';

export const routes: Routes = [
  // Default route to the dashboard
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  {
    path: 'dashboard',
    component: DashboardComponent,
    title: 'Energy Dashboard' // Set a title for the route
  },
  // You can add more routes here later
  // { path: 'settings', component: SettingsComponent, title: 'Settings' },
  { path: '**', redirectTo: '/dashboard' } // Wildcard route for a 404 or redirect
];
