1) Find songs from a specific artist and order them by ascending streams.
```
PREFIX music: <http://www.semanticweb.org/music_ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?track ?name ?trackname ?streams ?mode
WHERE {
    ?artist rdf:type music:Artist .
    ?track rdf:type music:Track .
    ?artist music:hasArtistName ?name .
    filter (STR(?name) = "Taylor Swift") 
    ?track music:performedBy ?artist . 
    ?track music:hasTrackName ?trackname .
    ?track music:hasStreams ?streams .
    ?track music:hasMusicDetails ?details .
    ?details music:hasMode ?mode
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
