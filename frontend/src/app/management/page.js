"use client";

import React from 'react';
import { useEffect, useState } from 'react';
import Header from '../../components/header';
import InfoCard from '../../components/infocard';
import TpsTable from './tpsTable';
import Footer from '../../components/footer';
import WithAuth from '@/components/withAuth';


function Management() {

    const [totalDistance, setTotalDistance] = useState(null);

    useEffect(() => {
        const fetchRouteData = async () => {
            try {
                // const response = await fetch('http://localhost:8080/route/latest');
                const response = await fetch('http://13.210.129.9/route/latest');
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
            <div className="flex flex-col min-h-screen bg-gray-50">
                <Header />
                <main className="flex flex-col items-center w-full px-4 md:px-10 py-5">
                    <div className="w-full max-w-5xl space-y-6">
                        {/* Centered Info Cards */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                        </div>
                        {/* Table */}
                        <TpsTable />
                    </div>
                </main>
                <Footer />
            </div>
        </WithAuth>
    );
}

export default Management;
