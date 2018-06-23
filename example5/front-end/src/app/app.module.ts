import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { MenuComponent } from './menu/menu.component';

@NgModule({
	declarations: [
		AppComponent,
		MenuComponent
	],
	imports: [
		BrowserModule,
		HttpClientModule,
		NgbModule.forRoot()
	],
	providers: [],
	bootstrap: [AppComponent]
})
export class AppModule { }
