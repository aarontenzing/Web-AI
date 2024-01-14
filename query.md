1) Find songs with some details, filtered on a specific artist name and order them by ascending streams.
```
PREFIX music: <http://www.semanticweb.org/music_ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?track ?name ?trackname ?streams
WHERE {
    ?artist rdf:type music:Artist .
    ?track rdf:type music:Track .
    ?artist music:hasArtistName ?name .
    filter (STR(?name) = "Taylor Swift") 
    ?track music:performedBy ?artist . 
    ?track music:hasTrackName ?trackname .
    ?track music:hasStreams ?streams .
    ?track music:relatesTrackToMusicDetails ?details .
    ?detail music:hasMode ?mode
}
ORDER BY ASC(?streams) 
```
2) Find how many songs are made by an artist and order them descending.
```
PREFIX music: <http://www.semanticweb.org/music_ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?name (COUNT(?track) AS ?total_tracks) 
WHERE {
    ?artist rdf:type music:Artist .
    ?track music:performedBy ?artist .
    ?artist music:hasArtistName ?name 
}
GROUP BY ?name
ORDER BY DESC(?total_tracks)
```
3) Find all the ranking one songs in the spotify charts and display their track name and artist name.
```
PREFIX music: <http://www.semanticweb.org/music_ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <http://www.semanticweb.org/music_ontology/>

SELECT DISTINCT (?rank as ?spotify_chart_rank) ?track_name ?artist_name
WHERE {
    ?chart rdf:type music:Chart .
    ?chart ex:rankedInSpotify ?rank .
    filter(?rank != 0 && ?rank <= 3)
    ?chart ex:chartContains ?track .
    ?track ex:hasTrackName ?track_name .
    ?track ex:performedBy ?artist .
    ?artist ex:hasArtistName ?artist_name .
}
```
4) Here I retrieve all the songs made by Justing Bieber ordered by the released year.
```
PREFIX ex: <http://www.semanticweb.org/music_ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?track ?trackName ?releaseYear ?streams ?albumName
WHERE {
  ?track rdf:type ex:Track ;
         ex:hasArtistId ?artistId ;
         ex:hasTrackName ?trackName ;
         ex:hasReleaseYear ?releaseYear ;
         ex:hasStreams ?streams ;
         ex:hasAlbumName ?albumName ;
         ex:performedBy ?artist .
    FILTER(?releaseYear != 0)

  ?artist rdf:type ex:Artist ;
          ex:hasArtistName "Justin Bieber"^^rdfs:literal .
}
ORDER BY ?releaseYear
```