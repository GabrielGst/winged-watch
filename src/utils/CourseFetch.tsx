export default async function FetchCourse( filename: string ) {
  let content;
  
  async function getData() {
    // const url = "http://localhost:3000/test.txt";
    const url = "http://localhost:3000/" + filename;
    console.log(url);
    try {
      const response = await fetch(url);
      if (!response.ok) {
        console.log(`Response not okay : ${response.status}`);
        throw new Error(`Response status: ${response.status}`);
      }

      // content = await response.text();
      content = await response.json();
      console.log(`Response is okay : ${content}`);
    } catch (error: any) {
      console.error(`Error in fetching url : ${error.message}`);
    }
  }

  await getData();

  return content
  // return (
  //   <p>
  //     {content}
  //   </p>
  // )
}
