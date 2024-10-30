"use client";

import React, { useEffect, useState } from 'react';

function TpsTable() {
    const [tpsData, setTpsData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://localhost:8080/tps');
                const data = await response.json();
                const formattedData = Object.keys(data).map((key) => ({
                    id: key,
                    ...data[key],
                }));
                setTpsData(formattedData);
            } catch (error) {
                console.error('Error fetching TPS data:', error);
            }
        };
        fetchData();
    }, []);

    return (
        <section className="flex flex-col px-4 py-3 w-full text-sm min-h-[432px]">
            <div className="overflow-hidden bg-white rounded-xl border border-gray-300 shadow-sm">
                <header className="hidden md:flex items-center bg-gray-100 font-medium text-gray-800 py-4 px-6 border-b border-gray-300">
                    <div className="w-1/4">Name</div>
                    <div className="w-1/2">Address</div>
                    <div className="w-1/6">Google Maps</div>
                    <div className="w-1/6">Capacity</div>
                    <div className="w-1/6">Last Emptied</div>
                </header>
                <div className="flex flex-col text-gray-700">
                    {tpsData.map((tps) => (
                        <div key={tps.id} className="flex flex-col md:flex-row items-start md:items-center w-full px-4 md:px-6 py-4 border-b border-gray-200 hover:bg-gray-50">
                            <div className="w-full md:w-1/4 font-semibold text-gray-800 md:font-normal md:text-gray-700" title={tps.name}>{tps.name}</div>
                            <div className="w-full md:w-1/2 truncate text-gray-600" title={tps.address}>{tps.address}</div>
                            <div className="w-full md:w-1/6 mt-2 md:mt-0 text-blue-600">
                                <a href={tps.gmapsLink} target="_blank" rel="noopener noreferrer" className="underline">
                                    View on Maps
                                </a>
                            </div>
                            <div className="w-full md:w-1/6 mt-2 md:mt-0">{tps.capacity || 'Default Capacity'}</div>
                            <div className="w-full md:w-1/6 mt-2 md:mt-0">{tps.lastEmptied || 'Default Last Emptied'}</div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

export default TpsTable;
