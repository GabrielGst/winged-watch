import MapWGS84 from "@/components/MapWGS84";
import Header from "@/components/Header";

// import { buildWindLayer } from "@/components/MapFetcher";


export default async function Home() {
  // const windLayer = await buildWindLayer();

  return (
    <div className="grid grid-rows-[20px_1fr_10px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Compute course !</button>
      <MapWGS84 /> 
    </div>
  );
}
