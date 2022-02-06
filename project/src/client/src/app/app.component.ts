import { SelectorMatcher } from '@angular/compiler';
import { Component } from '@angular/core';
import { HttpClient, HttpHeaders, HttpClientModule} from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {
  title = 'DAAR Projet Online Library Search Engine';
  public searchString: string;
  public ids: number[];
  public titles: string[];
  public authors: string[];
  public dates: string[];
  public scores: string[];
  public suggestionsIds: string[];
  public suggestionsTitles: string[];
  public suggestionsAuthors: string[];
  public suggestionsDates: string[];
  public noSuggestion: boolean;
  constructor(private http: HttpClient ) 
  {
    this.searchString = ""
    this.ids = []
    this.titles = []
    this.authors = []
    this.dates = []
    this.scores = []
    
    this.suggestionsIds = []
    this.suggestionsTitles = []
    this.suggestionsAuthors = []
    this.suggestionsDates = []
    this.noSuggestion = false
    
  }

  search(){    
    const httpOptions = {
      headers: new HttpHeaders({ 
        'Access-Control-Allow-Origin':'*'
      })
    };
    
    var res = this.http.get<any>('http://127.0.0.1:8000/search?q='+this.searchString, httpOptions).subscribe({
      next: data => {
        this.ids = []
        this.titles = []
        this.authors = []
        this.dates = []
        this.scores = []
        
        let results = data.res
        
        var sortedResults = results.sort((obj1:any, obj2:any) => {
          var o1: number = +obj1.score;
          var o2: number = +obj2.score;
          if (o1 > o2) {return -1;}
          if (o1 < o2) {return 1;}
          return 0;
        });
        
        for (let entry of sortedResults) {
          this.ids.push(entry.id)
          this.titles.push(entry.Title)
          this.authors.push(entry.Author)
          this.dates.push(entry.Release_Date)
          this.scores.push(entry.score)
        }
      },
      error: error => {
        console.error('There was an error!', error);
      }
    })
  }

  suggest(id:any){    
    const httpOptions = {
      headers: new HttpHeaders({ 
        'Access-Control-Allow-Origin':'*'
      })
    };
    
    var res = this.http.get<any>('http://127.0.0.1:8000/suggest?q='+id, httpOptions).subscribe({
      next: data => {
        this.suggestionsIds = []
        this.suggestionsTitles = []
        this.suggestionsAuthors = []
        this.suggestionsDates = []
        this.noSuggestion = false
         
        let results = data.res
        if (results.length == 0){
          this.noSuggestion = true
        }
        else{
          for (let entry of results) {
            this.suggestionsIds.push(entry.id)
            this.suggestionsTitles.push(entry.Title)
            this.suggestionsAuthors.push(entry.Author)
            this.suggestionsDates.push(entry.Release_Date)
          }  
        }
      },
      error: error => {
        console.error('There was an error!', error);
      }
    })
  }
}
