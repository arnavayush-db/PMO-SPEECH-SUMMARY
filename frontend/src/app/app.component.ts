import { Component, OnInit } from '@angular/core';
import { SpeechService } from './speech.service';
import { Speech } from './speech.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  speeches: Speech[] = [];
  loading = false;
  error: string | null = null;

  constructor(private speechService: SpeechService) {}

  ngOnInit() {
    this.loadSpeeches();
  }

  loadSpeeches() {
    this.loading = true;
    this.error = null;
    this.speechService.getSpeeches().subscribe({
      next: (speeches) => {
        this.speeches = speeches;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load speeches. Please try again later.';
        this.loading = false;
        console.error(err);
      }
    });
  }
}