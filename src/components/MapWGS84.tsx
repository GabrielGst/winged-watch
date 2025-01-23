// https://openlayers.org/en/latest/examples/reprojection-wgs84.html

'use client';

import { useEffect, useRef } from 'react';
import 'ol/ol.css';
import Map from 'ol/Map.js';
import OSM from 'ol/source/OSM.js';
import TileLayer from 'ol/layer/Tile.js';
import View from 'ol/View.js';

const MapWGS84 = ({ setMapObject }: { setMapObject: (map: Map | undefined) => void }) => {
  const mapContainer = useRef<HTMLDivElement | null>(null);
  // on component mount create the map and set the map references to the state
  useEffect(() => {
    const map = new Map({
      layers: [
        new TileLayer({
          source: new OSM(),
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
    <div ref={mapContainer} className="w-full h-96"></div>
  );
};

export default MapWGS84;