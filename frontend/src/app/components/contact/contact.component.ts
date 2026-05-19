import { Component, ElementRef, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import emailjs from '@emailjs/browser';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './contact.component.html',
  styleUrl: './contact.component.css'
})
export class ContactComponent implements OnInit {
  form = {
    name: '',
    email: '',
    subject: 'This message from portfolio',
    message: '',
  };
  submitted = signal(false);
  sending = signal(false);
  error = signal('');

  contactCards = [
    { icon: '📍', label: 'Address', value: 'Hyderabad, Telangana, India' },
    { icon: '📞', label: 'Phone', value: '+91 9052244239' },
    { icon: '📧', label: 'Email', value: 'avinashgembali13@gmail.com' },
  ];

  constructor(private el: ElementRef) {
    emailjs.init(environment.emailjs.publicKey);
  }

  ngOnInit() {
    const observer = new IntersectionObserver(
      entries => entries.forEach(e => e.isIntersecting && e.target.classList.add('visible')),
      { threshold: 0.1 }
    );
    setTimeout(() => {
      this.el.nativeElement.querySelectorAll('.animate-on-scroll').forEach((el: Element) => observer.observe(el));
    }, 100);
  }

  async onSubmit() {
    this.sending.set(true);
    this.error.set('');
    try {
      await emailjs.send(environment.emailjs.serviceId, environment.emailjs.templateId, {
        from_name: this.form.name,
        from_email: this.form.email,
        subject: this.form.subject,
        message: this.form.message,
        to_email: 'avinashgembali13@gmail.com',
        reply_to: this.form.email,
      });
      this.submitted.set(true);
      this.form = { name: '', email: '', subject: 'This message from portfolio', message: '' };
    } catch {
      this.error.set('Failed to send message. Please try again.');
    } finally {
      this.sending.set(false);
    }
  }
}
