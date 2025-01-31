// https://openlayers.org/en/latest/examples/reprojection-wgs84.html
// https://openlayers.org/en/latest/examples/wind-arrows.html

'use client';

import { useEffect, useRef } from 'react';
import 'ol/ol.css';
import Map from 'ol/Map.js';
import OSM from 'ol/source/OSM.js';
import TileLayer from 'ol/layer/Tile.js';
import View from 'ol/View.js';


// https://openlayers.org/en/latest/examples/wind-arrows.html

import Feature from 'ol/Feature.js';
import Point from 'ol/geom/Point.js';
import VectorLayer from 'ol/layer/Vector.js';
import VectorSource from 'ol/source/Vector.js';
import {Fill, RegularShape, Stroke, Style} from 'ol/style.js';
import {fromLonLat} from 'ol/proj.js';
import { Geometry } from 'ol/geom';



const shaft = new RegularShape({
  points: 2,
  radius: 5,
  stroke: new Stroke({
    width: 2,
    color: 'black',
  }),
  rotateWithView: true,
});

const head = new RegularShape({
  points: 3,
  radius: 5,
  fill: new Fill({
    color: 'black',
  }),
  rotateWithView: true,
});

const styles = [new Style({image: shaft}), new Style({image: head})];

// const source = new VectorSource({
//   attributions:
//     'Weather data by ecmwf',
// });


// This function gets called at build time on server-side.
// It won't be called on client-side, so you can even do
// direct database queries.
export async function getStaticProps() {
  const source = new VectorSource({
    attributions:
      'Weather data by ecmwf',
  });

  // Call an external API endpoint to get posts.
  // You can use any data fetching library
  const res = await fetch('./api/dataset/wind.json')
  const posts = await res.json()
  // console.log("lol")
  const features: Feature<Geometry>[] = [];

  posts.forEach(function (report: { [x: string]: any; coord?: any; }) { // data.list
    const feature = new Feature(
      new Point(fromLonLat([report.longitude, report.latitude])),
    );
    feature.setProperties(report);
    features.push(feature);
  });

  source.addFeatures(features);
  // console.log(source.getExtent())
 
  // By returning { props: { posts } }, the Blog component
  // will receive `posts` as a prop at build time
  return {
    props: {
      source,
    },
  }
}



const MapWGS84 = ({ setMapObject, source }: { setMapObject: (map: Map | undefined) => void, source: VectorSource }) => {
  const mapContainer = useRef<HTMLDivElement | null>(null);


  // on component mount create the map and set the map references to the state
  useEffect(() => {
    const map = new Map({
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
        new VectorLayer({
          source: source,
          style: function (feature) {
            // const wind = feature.get('wind');
            // rotate arrow away from wind origin
            // const angle = ((wind.deg - 180) * Math.PI) / 180;
            // const scale = wind.speed / 10;
            const angle = feature.get("deg")
            const scale = feature.get("speed") / 10
            shaft.setScale([1, scale]);
            shaft.setRotation(angle);
            head.setDisplacement([
              0,
              head.getRadius() / 2 + shaft.getRadius() * scale,
            ]);
            head.setRotation(angle);
            return styles;
          },
        }),
      ],
      // target: 'map',
      view: new View({
        projection: 'EPSG:4326',
        center: [0, 0],
        zoom: 2,
      }),
    });

    // const windDataFetch = () => {
    //   fetch('./api/dataset/wind.json')
    //     .then(function (response) {
    //       return response.json();
    //     })
    //     .then(function (data) {
    //       const features: Feature<Geometry>[] = [];
    //       data.forEach(function (report: { [x: string]: any; coord?: any; }) { // data.list
    //         const feature = new Feature(
    //           new Point(fromLonLat([report.longitude, report.latitude])),
    //         );
    //         feature.setProperties(report);
    //         features.push(feature);
    //       });
    //       source.addFeatures(features);
    //       map.getView().fit(source.getExtent());
    //     });
    //   };

    if (mapContainer.current) {
      map.setTarget(mapContainer.current);
    }

    setMapObject(map);
    // map.getView().fit(source.getExtent());

    // on component unmount remove the map refrences to avoid unexpected behaviour
    return () => {
      map.setTarget(undefined);
      setMapObject(undefined);
    };
  }, []);
  

  return (
    <div ref={mapContainer} className="w-full h-full"></div>
  );
};

export default MapWGS84;