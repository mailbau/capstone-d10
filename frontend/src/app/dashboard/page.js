import React from 'react';
import Header from '../../components/header';
import InfoCard from '../../components/infocard';
import Footer from '../../components/footer';

function DashboardPage() {
    return (
        <div className="flex overflow-hidden flex-col bg-white">
            <Header />
            <main className="flex justify-center items-start px-40 py-5 w-full min-h-[931px] max-md:px-5 max-md:max-w-full">
                <div className="flex flex-col min-h-[891px] min-w-[240px] w-[960px] max-md:max-w-full">
                    {/* Info Card */}
                    <InfoCard
                        title="Total Distance"
                        description="The total distance of the optimal garbage collection route is 50 miles."
                    />
                    <InfoCard
                        title="Emission Information"
                        description="The emission information for the optimal garbage collection route is 5 tons of CO2."
                    />
                    {/* Map */}
                    <section className="flex items-start px-4 py-3 max-w-full min-h-[546px] w-[960px]">
                        <img loading="lazy" src="/tempmap.png" alt="Waste Management Route Map" className="object-contain rounded-xl aspect-[1.78] min-w-[240px] w-[928px]" />
                    </section>
                    {/* Buttons */}
                    <section className="flex items-start px-4 py-3 w-full text-sm font-bold tracking-wide max-w-[960px] min-h-[64px] max-md:max-w-full">
                        <div className="flex gap-3 px-px min-w-[240px] w-[318px]">
                            <button className="flex justify-center items-start text-white min-h-[40px]">
                                <span className="flex overflow-hidden justify-center items-center px-4 bg-emerald-600 rounded-3xl min-h-[40px] w-[129px]">
                                    Update Route
                                </span>
                            </button>
                            <button className="flex justify-center items-start min-h-[40px] text-stone-900">
                                <span className="flex overflow-hidden justify-center items-center px-4 bg-lime-50 rounded-3xl min-h-[40px] w-[178px]">
                                    Send Route to Phone
                                </span>
                            </button>
                        </div>
                    </section>
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default DashboardPage;