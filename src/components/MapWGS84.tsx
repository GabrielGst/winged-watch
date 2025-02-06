"use client";

// https://openlayers.org/en/latest/examples/reprojection-wgs84.html
// https://openlayers.org/en/latest/examples/wind-arrows.html

import { useRef, useState, useEffect } from 'react';
import 'ol/ol.css';
import Map from 'ol/Map.js';
import OSM from 'ol/source/OSM.js';
import TileLayer from 'ol/layer/Tile.js';
import View from 'ol/View.js';
import VectorLayer from 'ol/layer/Vector';
// import { after } from 'next/server'

// import { buildWindLayer } from "@/components/MapFetcher";
import 'ol/ol.css';
import Feature from 'ol/Feature.js';
import Point from 'ol/geom/Point.js';
import VectorSource from 'ol/source/Vector.js';
import {Fill, RegularShape, Stroke, Style} from 'ol/style.js';
import GeoJSON from 'ol/format/GeoJSON.js';
import {fromLonLat} from 'ol/proj.js';
import { Geometry } from 'ol/geom';

import GetText from '@/utils/TextFetchTest'
import BuildWindLayer from '@/utils/MapFetcher';
import { use } from "react";

// { setMapObject }: { setMapObject: (map: Map | undefined) => void }
// { windLayer }: {windLayer: VectorLayer}
const MapWGS84 = () => {
  const [text, setText] = useState<number>(0);
  const [layer, setLayer] = useState<VectorLayer>(new VectorLayer());
  // const [source, setSource] = useState<VectorSource>(new VectorSource());
  const source = new VectorSource({});

  // Define styles
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
  

  useEffect(() => {

    async function fetchData() {
      const res = await GetText();

      if (res) {
        const results = (Object.values(res) as { [x: string]: number }[]);
        const result = results[0];
        // setText(result.longitude);
        // console.log(`text: ${result.longitude}`);
        
        // const features: Feature<Geometry>[] = [];
        // const sourceBis = new VectorSource({});

        results.forEach(function (report) {
          if (report.longitude !== undefined && report.latitude !== undefined) {
            const feature = new Feature({geometry: new Point(fromLonLat([report.longitude, report.latitude], 'EPSG:4326'))});
            const geometry = feature.getGeometry();

            if (geometry) {
              feature.set("speed", report.speed);
              feature.set("deg", report.deg);
              // console.log(`Feature: ${feature.getKeys()}`);
              // console.log(`Feature: ${feature.get("speed")}`);
              // console.log(`Feature: ${feature.get("deg")}`);

              // features.push(feature);
              source.addFeature(feature);
            } else {
              console.error('Feature geometry is undefined');
            }
            
          } else {
            console.error('Invalid report data:', report);
          }
        });

        // console.log(`Features length: ${features.length}`);
        // console.log(`Source length: ${source.getFeatures().length}`);
        // console.log(`Source [0]: ${source.getFeatures()[0].getKeys()}`);

        // if (features.length > 0) {
        //   // sourceBis.addFeatures(features);

        //   // setSource(sourceBis);
          
        //   // console.log(`Source length: ${source.getFeatures().length}`);
        // } else {
        //   console.warn('No features created from results.');
        // }
      }

      // const res2  = await BuildWindLayer();

      // if (res2) {
      //   setLayer(res2.vLayer);
      //   setSource(res2.source);
      //   console.log(`Fetched layer: ${res2.vLayer}`);
      //   console.log(`Fetched source: ${res2.source}`);
      //   const features = res2.source.getFeatures();
      //   const feature = features[0];

      //   console.log('Feature 0:', feature);
      // }


    }

    fetchData();

    const map = new Map({
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
        new VectorLayer({
          source: source,
          // style: null,
          style: function (feature) {
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
      target: 'map',
      view: new View({
        projection: 'EPSG:4326',
        center: [0, 0],
        zoom: 2,
      }),
    });

    // map.addLayer(layer);
    // map.getView().fit(source.getExtent());

    // on component unmount remove the map refrences to avoid unexpected behaviour
    return () => {
      map.setTarget(undefined);
      // setMapObject(undefined);
    };

  }, []);

  // useEffect(() => {
    // const test = source.getFeatures()[0];
    // console.log(`Test: ${test.get("longitude")}`);
    // console.log(`Test: ${test.getProperties().longitude}`);

    // const map = new Map({
    //   layers: [
    //     new TileLayer({
    //       source: new OSM(),
    //     }),
    //     new VectorLayer({
    //       source: source,
    //       style: function (feature) {
    //         const angle = feature.get("deg")
    //         const scale = feature.get("speed")
    //         shaft.setScale([1, scale]);
    //         shaft.setRotation(angle);
    //         head.setDisplacement([
    //           0,
    //           head.getRadius() / 2 + shaft.getRadius() * scale,
    //         ]);
    //         head.setRotation(angle);
    //         return styles;
    //       },
    //     }),
    //   ],
    //   target: 'map',
    //   view: new View({
    //     projection: 'EPSG:4326',
    //     center: [0, 0],
    //     zoom: 2,
    //   }),
    // });

    // // map.addLayer(layer);
    // map.getView().fit(source.getExtent());

    // // on component unmount remove the map refrences to avoid unexpected behaviour
    // return () => {
    //   map.setTarget(undefined);
    //   // setMapObject(undefined);
    // };
  // }, [source]);
    
  // console.log(layer)

  return (
    <div id='map' className="w-full h-full"></div>
  );
};

export default MapWGS84;