import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter, withViewTransitions } from '@angular/router';
import { HttpClientModule } from '@angular/common/http'; // Import HttpClientModule
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withViewTransitions()), // Add withViewTransitions for nice route changes
    importProvidersFrom(HttpClientModule), // Provide HttpClientModule for data service
    provideAnimationsAsync() // For Angular Material animations if you add it later, or other animation libraries
  ]
};
