import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { MenuComponent } from './menu/menu.component';
import { SigninComponent } from './signin/signin.component';
import { MessagesComponent } from './messages/messages.component';
import { LoggingInterceptor } from './http.interceptor';

@NgModule({
	declarations: [
		AppComponent,
		MenuComponent,
		SigninComponent,
		MessagesComponent
	],
	imports: [
		BrowserModule,
		NgbModule.forRoot(),
		HttpClientModule,
	],
	providers: [
		// {
		// 	provide: HTTP_INTERCEPTORS,
		// 	useClass: LoggingInterceptor,
		// 	multi: true
		// }
	],
	bootstrap: [AppComponent]
})
export class AppModule { }
