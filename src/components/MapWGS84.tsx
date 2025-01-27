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

const source = new VectorSource({
  attributions:
    'Weather data by ecmwf',
});

const map = new Map({
  layers: [
    new TileLayer({
      source: new OSM(),
    }),
    new VectorLayer({
      source: source,
      style: function (feature) {
        const wind = feature.get('wind');
        // rotate arrow away from wind origin
        const angle = ((wind.deg - 180) * Math.PI) / 180;
        const scale = wind.speed / 10;
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
  target: 'map',
  view: new View({
    center: [0, 0],
    zoom: 2,
  }),
});

// fetch('../api/data.json')
//   .then(function (response) {
//     return response.json();
//   })
//   .then(function (data) {
//     const features = [];
//     data.list.forEach(function (report) {
//       const feature = new Feature(
//         new Point(fromLonLat([report.coord.lon, report.coord.lat])),
//       );
//       feature.setProperties(report);
//       features.push(feature);
//     });
//     source.addFeatures(features);
//     map.getView().fit(source.getExtent());
//   });






const MapWGS84 = ({ setMapObject }: { setMapObject: (map: Map | undefined) => void }) => {
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
            const wind = feature.get('wind');
            // rotate arrow away from wind origin
            const angle = ((wind.deg - 180) * Math.PI) / 180;
            const scale = wind.speed / 10;
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

    if (mapContainer.current) {
      map.setTarget(mapContainer.current);
    }

    setMapObject(map);

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