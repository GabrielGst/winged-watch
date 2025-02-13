<!-- <h1 align="center">Wind Watch</h1> -->
<div align="center">
  <img src="/public/Style/wind-watch.jpg">
</div>

<h4 align="center">Web app for computing optimized wind-based sailing courses.</h4>

<!-- <h1 align="center"> </h1> -->

<!-- ![version](https://img.shields.io/badge/version-0.0.1-blueviolet) -->
<div style="flex" align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blueviolet" alt="version badge">
  <img src="https://img.shields.io/badge/development-in%20progress-orange" alt="Development Status">
  <img src="https://img.shields.io/badge/maintained-yes-brightgreen.svg" alt="Maintenance Status">
  <img src="https://img.shields.io/badge/launched-no-red.svg" alt="Launch Status">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License">

</div>

<!-- ![development](https://img.shields.io/badge/development-in%20progress-orange)
![maintenance](https://img.shields.io/badge/maintained-yes-brightgreen.svg)
![launched](https://img.shields.io/badge/launched-no-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue) -->

## Introduction

Winged Watch is a student project that aims to provide real-time meteorological forecasts and sailing course optimization. Please notice that this project is experimental and should not be used in practice by sailor. Our goal is to deliver a robust and scalable solution that meets the needs of amateur sailors, and in the long-tern, modern shipping enterprises that would want to benchmark wind-propulsion solutions on their ships.

### Goals

- Real-time data monitoring
- Advanced analytics and reporting
- Scalable and flexible architecture
- User-friendly interface

### Project structure & description

We implemented a web app using a node server with a nextjs framework running on a vps. The server communicates through `HTTP GET` and `HTTP POST` requests with a python flask server running on the same vps. The flask server daily performs the retrieve of the forecast from ECMWF Medium Range  <https://www.ecmwf.int/en/forecasts/documentation-and-support/medium-range-forecasts>, using multithreading to handle processing of datafiles while keeping the communication with the node server real time.

The app allow the user to display the wind forecast, select start and end points of a sail trip and ask for the optimized course to be computed and presented on the client side. The client handles basics navigation requests as well as storing trip's information before sending them to the flask backend when fired by the user. Some components are rendered server side while pages and other components are rendered client side for responsivity.

```shell
.
├── README.md                       # README file
├── .github                         # GitHub folder
├── .venv                           # Python virtual environment
├── .next                           # next cache (created on build)
├── .vscode                         # VSCode configuration
├── api                             # Python flask server & dependencies
│   ├── requirements.txt            # Python requeriments
│   ├── index.py                    # Python main
│   ├── Tests                       # Unit python test functions
├── public                          # Public assets folder
├── src
│   ├── app                         # Next JS App (App Router)
│   ├── components                  # React components
│   ├── utils                       # Utilities folder
├── tailwind.config.js              # Tailwind CSS configuration
└── tsconfig.json                   # TypeScript configuration
```

## Getting Started

### Requirements

#### Python

- Python 3.12+
- Required Libraries: see `requirements.txt`

#### Node.js

- Node.js 20+
- `npm` & `pnpm`
- Required Packages: see `package.json`

### Installation

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

Run the following command on your local environment:

```shell
git clone --depth=1 https://github.com/GabrielGst/winged-watch.git my-project-name
cd my-project-name
npm install
```

First, run the Flask intall:

```bash
npm run flask-install
```

Second, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file. This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Debugging & Testing


All unit tests are located alongside the source code in the same directory, making them easier to find. Tests arer only available for the Python server. You can run the tests with the following command:

```shell
.venv\Scripts\activate # on Windows
.venv\bin\activate # on Unix

python -m unittest [function-to-test].py
```

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## Deploy to production

For vps users only. Log into your vps then clone the repo. Then follow the _Getting Started_ section to install the server, and checks firewall rules to open your selected ports.

## Contributions

Everyone is welcome to contribute to this project. Feel free to open an issue if you have any questions or find a bug. Totally open to suggestions and improvements.

### Future Implementation

- Bathymetric maps integration
- Tidal heightsd and current forecast integration
- Boats specification integration
- Loggin methods
- Shipyard implementation : register boats to be used
- Trips list : register trips onto the app for future analytics or sharing with friends

### Graphic Chart

#### Primary

# 172E73

#142559

#6CAFD9

#71BBD9

#F2F2F2

#### Secondary

#4F5F73

#8090A6

#93B3BF

#C9EBF2

#F2F2F2

### License

Licensed under the MIT License, Copyright © 2024

See [LICENSE](LICENSE) for more information.
