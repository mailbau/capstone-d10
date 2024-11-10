"use client"

import React, { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import Header from '../../components/header';
import InfoCard from '../../components/infocard';
import Footer from '../../components/footer';
import WithAuth from '@/components/withAuth';

const MapComponent = dynamic(() => import('./mapComponent'), { ssr: false });

function DashboardPage() {
    const [totalDistance, setTotalDistance] = useState(null);

    useEffect(() => {
        const fetchRouteData = async () => {
            try {
                // const response = await fetch('http://localhost:8080/route/latest');
                const response = await fetch('https://capstoned10.duckdns.org//route/latest');
                const data = await response.json();

                // Access the latest route data
                const latestRouteKey = Object.keys(data)[0];
                const latestRoute = data[latestRouteKey];

                if (latestRoute && latestRoute.total_distance) {
                    setTotalDistance(latestRoute.total_distance);
                } else {
                    console.error("No route data or total distance found.");
                }
            } catch (error) {
                console.error("Error fetching route data:", error);
            }
        };

        fetchRouteData();
    }, []);

    return (
        <WithAuth>
            <div className="flex flex-col bg-gray-50 min-h-screen">
                <Header />
                <main className="flex justify-center items-start px-4 py-10 w-full">
                    <div className="flex flex-col items-center w-full max-w-5xl space-y-8">
                        {/* Info Cards Section */}
                        <section className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
                            <InfoCard
                                title="Total Distance"
                                description={`The total distance of the optimal garbage collection route is ${totalDistance ? totalDistance.toFixed(2) + ' km' : 'loading...'}.`}
                                link="/totaldistance"
                            />
                            <InfoCard
                                title="Emission Information"
                                description={`The emission information for the optimal garbage collection route is ${totalDistance ? (totalDistance * 0.0010).toFixed(2) + ' tons of CO2' : 'loading...'
                                    }.`}
                                link="/emission"
                            />
                        </section>

                        {/* Map Section */}
                        <section className="w-full bg-white rounded-xl shadow-lg overflow-hidden">
                            <h2 className="text-xl font-semibold text-gray-800 px-6 pt-4 pb-2">Route Map</h2>
                            <div className="w-full h-60 md:h-80 lg:h-[400px]">
                                <MapComponent />
                            </div>
                        </section>

                        {/* Buttons Section */}
                        <section className="flex flex-col sm:flex-row gap-4 w-full justify-center">
                            <button
                                onClick={() => window.location.reload()}
                                className="flex items-center justify-center w-full sm:w-[150px] px-4 py-3 bg-emerald-600 text-white rounded-full font-semibold shadow-md hover:bg-emerald-700 transition duration-150">
                                Update Route
                            </button>
                        </section>
                    </div>
                </main>
                <Footer />
            </div>
        </WithAuth>
    );
}

export default DashboardPage;
