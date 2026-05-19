import { Component } from '@angular/core';

@Component({
  selector: 'app-hire-me',
  standalone: true,
  imports: [],
  templateUrl: './hire-me.component.html',
  styleUrl: './hire-me.component.css'
})
export class HireMeComponent {
  scrollTo(anchor: string) {
    document.getElementById(anchor)?.scrollIntoView({ behavior: 'smooth' });
  }
}
