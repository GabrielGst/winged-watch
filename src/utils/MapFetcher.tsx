import 'ol/ol.css';
import Feature from 'ol/Feature.js';
import Point from 'ol/geom/Point.js';
import VectorLayer from 'ol/layer/Vector.js';
import VectorSource from 'ol/source/Vector.js';
import {Fill, RegularShape, Stroke, Style} from 'ol/style.js';
import {fromLonLat} from 'ol/proj.js';
import { Geometry } from 'ol/geom';

export default async function BuildWindLayer() {
  
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
  
  
  // Define a source
  const source = new VectorSource({
    attributions:
      'Weather data by ecmwf',
  });
  
  // Update the source with fetched data
  async function getData() {
    const res =  await fetch('wind-sample-1000.json')
    if (!res.ok) {
      console.log("Response not okay.")
      throw new Error('Network response was not ok');
    } else {
      console.log("Parsing json.")
      const content = await res.json();
      const features: Feature<Geometry>[] = [];
      // content.forEach(function (report: { [x: string]: number }) { // data.list
      const point = (Object.values(content) as { [x: string]: number }[])[0]
      const feature = new Feature({geometry: new Point(fromLonLat([point.longitude, point.latitude]))});
      features.push(feature);
      // .forEach(function (report) {
      //   const feature = new Feature({
      //     geometry: new Point(fromLonLat([45, 13])),
      //   });
      //   // feature.setProperties(report);
      //   features.push(feature);
      // });
      source.addFeatures(features);
      // map.getView().fit(source.getExtent());
    }
  };

  getData()
  
  
  // Construct the vector layer
  const vLayer = new VectorLayer({
      source: source,
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
  })

  // Return the layer
  return{
    vLayer,
    source,
  }
}




  
  

  
  
  // // This function gets called at build time on server-side.
  // // It won't be called on client-side, so you can even do
  // // direct database queries.
  // export async function getStaticProps() {
  //   const source = new VectorSource({
  //     attributions:
  //       'Weather data by ecmwf',
  //   });
  
  //   // Call an external API endpoint to get posts.
  //   // You can use any data fetching library
  //   const res = await fetch('./api/dataset/wind.json')
  //   const posts = await res.json()
  //   // console.log("lol")
  //   const features: Feature<Geometry>[] = [];
  
  //   posts.forEach(function (report: { [x: string]: any; coord?: any; }) { // data.list
  //     const feature = new Feature(
  //       new Point(fromLonLat([report.longitude, report.latitude])),
  //     );
  //     feature.setProperties(report);
  //     features.push(feature);
  //   });
  
  //   source.addFeatures(features);
  //   // console.log(source.getExtent())
   
  //   // By returning { props: { posts } }, the Blog component
  //   // will receive `posts` as a prop at build time
  //   return {
  //     props: {
  //       source,
  //     },
  //   }
  // }

