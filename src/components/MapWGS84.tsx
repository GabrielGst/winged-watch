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
import 'ol/ol.css';
import Feature from 'ol/Feature.js';
import Point from 'ol/geom/Point.js';
import VectorSource from 'ol/source/Vector.js';
import {Fill, RegularShape, Stroke, Style} from 'ol/style.js';
import GeoJSON from 'ol/format/GeoJSON.js';
import {fromLonLat} from 'ol/proj.js';
import { Geometry } from 'ol/geom';
import { transform } from 'ol/proj';
import Draw from 'ol/interaction/Draw.js';

import GetText from '@/utils/TextFetchTest'
import FetchCourse from '@/utils/CourseFetch';
import BuildWindLayer from '@/utils/MapFetcher';
import { use } from "react";

const MapWGS84 = () => {
  const [serverResponse, setServerResponse] = useState<string | null>(null);
  const [text, setText] = useState<number>(0);
  const [layer, setLayer] = useState<VectorLayer>(new VectorLayer());
  const [path, setPath] = useState<number[][]>([]);
  const [map, setMap] = useState<Map>();

  function handleRegister() {
    sendDataToFlask(path);
  }

  const sendDataToFlask = (dataToSend: number[][]) => {
    fetch("http://localhost:3000/api/receive-data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: dataToSend , process: true}),
    })
      .then((response) => response.json())
      .then((result) => {
        console.log("Server response:", result);
        setServerResponse(result.message);
      })
      .catch((error) => {
        console.error("Error sending data:", error);
      });
  };

  const source = new VectorSource({});

  const sourceTrip = new VectorSource({wrapX: false});

  const vectorTrip = new VectorLayer({
    source: sourceTrip,
  });

  const sourceCourse = new VectorSource({wrapX: false});

  const vectorCourse = new VectorLayer({
    source: sourceCourse,
  });

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

    setMap(map);

    // map.addLayer(layer);
    // map.getView().fit(source.getExtent());

    // on component unmount remove the map refrences to avoid unexpected behaviour
    return () => {
      map.setTarget(undefined);
      // setMapObject(undefined);
    };

  }, []);

  let draw: Draw;

  function addTripPoint() {
     // global so we can remove it later
    function addInteraction() {
      draw = new Draw({
        source: sourceTrip,
        type: "Point",
      });
      if (map)
      map.addInteraction(draw);
    };
    addInteraction();
  }
  function handleUndo() {
    draw.removeLastPoint();
    path.pop();
  }

  addTripPoint();
  map?.addLayer(vectorTrip);

  if (map) {
    map.on('click', function(evt){
      // console.log(transform(evt.coordinate, 'EPSG:4326', 'EPSG:4326'));
      setPath([...path, transform(evt.coordinate, 'EPSG:4326', 'EPSG:4326')]);
  });
  }

  useEffect(() => {
    console.log(path);
  }, [path]);
  
  function handleShow() {
    async function fetchData() {
      const res = await FetchCourse("course.json");

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

              sourceCourse.addFeature(feature);
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
  }
  
  map?.addLayer(vectorCourse);


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

    <div className="grid grid-rows-[20px_1fr_10px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
    <p className="text-2xl font-bold">Map</p>
    <div id='map' className="w-full h-full"></div>
    <div className='flex flex-row'>
      <button id='undo' className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'onClick={ handleUndo }>Undo</button>
      <button id='send' className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded' onClick={ handleRegister }>Register trip and compute course</button>
      <button id='show' className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded' onClick={ handleShow }>Show course</button>
    </div>
  </div>
  );
};

export default MapWGS84;