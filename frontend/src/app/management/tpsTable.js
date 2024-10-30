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
        <section className="flex flex-col justify-center px-4 py-3 w-full text-sm min-h-[432px]">
            <div className="flex overflow-hidden flex-col w-full bg-white rounded-xl border border-solid border-stone-300 min-h-[408px]">
                <div className="flex flex-col w-full min-h-[406px]">
                    <header className="flex flex-col w-full font-medium text-stone-900 max-md:max-w-full">
                        <div className="flex flex-wrap items-start w-full bg-white min-h-[46px]">
                            <div className="flex flex-col grow shrink justify-center px-4 py-3.5 min-h-[46px] w-[220px]"> {/* Increased width */}
                                <span className="max-w-full min-h-[21px] w-[215px]">Name</span>
                            </div>
                            <div className="flex flex-col grow shrink justify-center px-4 py-3.5 min-h-[46px] w-[420px]"> {/* Increased width */}
                                <span className="max-w-full min-h-[21px] w-[410px]">Address</span>
                            </div>
                            <div className="flex flex-col grow shrink justify-center items-center px-4 py-3.5 whitespace-nowrap min-h-[46px] w-[200px]"> {/* Increased width */}
                                <span className="max-w-full min-h-[21px] w-[195px]">Google Maps</span>
                            </div>
                            <div className="flex flex-col grow shrink justify-center items-center px-4 py-3.5 whitespace-nowrap min-h-[46px] w-[200px]"> {/* New column */}
                                <span className="max-w-full min-h-[21px] w-[195px]">Capacity</span>
                            </div>
                            <div className="flex flex-col grow shrink justify-center items-center px-4 py-3.5 whitespace-nowrap min-h-[46px] w-[200px]"> {/* New column */}
                                <span className="max-w-full min-h-[21px] w-[195px]">Last Emptied</span>
                            </div>
                        </div>
                    </header>
                    <div className="flex flex-col w-full max-w-full min-h-[360px] text-stone-500 max-md:max-w-full">
                        {tpsData.map((tps) => (
                            <div key={tps.id} className="flex flex-wrap items-start w-full border-t border-gray-200 min-h-[72px]">
                                <div className="flex flex-col grow shrink justify-center items-center px-4 py-7 min-h-[72px] text-stone-900 w-[220px]"> {/* Adjusted for consistency */}
                                    <span className="max-w-full min-h-[21px] w-[215px]">{tps.name}</span>
                                </div>
                                <div className="flex flex-col grow shrink justify-center items-center px-4 py-7 min-h-[72px] w-[420px]"> {/* Adjusted for consistency */}
                                    <span className="max-w-full min-h-[21px] w-[410px]" title={tps.address}>{tps.address}</span>
                                </div>
                                <div className="flex flex-col grow shrink justify-center items-start px-4 py-7 whitespace-nowrap min-h-[72px] w-[169px]">
                                    <a href={tps.gmapsLink} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
                                        View on Maps
                                    </a>
                                </div>
                                <div className="flex flex-col grow shrink justify-center items-center px-4 py-7 whitespace-nowrap min-h-[72px] w-[200px]"> {/* New column */}
                                    <span className="max-w-full min-h-[21px] w-[195px]">Default Capacity</span>
                                </div>
                                <div className="flex flex-col grow shrink justify-center items-center px-4 py-7 whitespace-nowrap min-h-[72px] w-[200px]"> {/* New column */}
                                    <span className="max-w-full min-h-[21px] w-[195px]">Default Last Emptied</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}

export default TpsTable;
