import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Speech } from './speech.model';

@Injectable({
  providedIn: 'root'
})
export class SpeechService {
  private apiUrl = 'http://localhost:3000/api/speeches';

  constructor(private http: HttpClient) {}

  getSpeeches(): Observable<Speech[]> {
    return this.http.get<Speech[]>(this.apiUrl);
  }
}