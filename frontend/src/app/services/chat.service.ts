import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface ChatMessage {
  role: 'user' | 'bot';
  text: string;
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  private readonly apiUrl = `${environment.apiUrl}/chat`;

  constructor(private http: HttpClient) {}

  ask(message: string): Observable<{ answer: string }> {
    return this.http.post<{ answer: string }>(this.apiUrl, { message });
  }
}
