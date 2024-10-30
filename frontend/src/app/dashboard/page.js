import React from 'react';
import Header from '../../components/header';
import InfoCard from '../../components/infocard';
import Footer from '../../components/footer';

function DashboardPage() {
    return (
        <div className="flex flex-col bg-gray-50 min-h-screen">
            <Header />
            <main className="flex justify-center items-start px-4 py-10 w-full">
                <div className="flex flex-col items-center w-full max-w-5xl space-y-8">
                    {/* Info Cards Section */}
                    <section className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
                        <InfoCard
                            title="Total Distance"
                            description="The total distance of the optimal garbage collection route is 50 miles."
                            link="/totaldistance"
                        />
                        <InfoCard
                            title="Emission Information"
                            description="The emission information for the optimal garbage collection route is 5 tons of CO2."
                            link="/emission"
                        />
                    </section>

                    {/* Map Section */}
                    <section className="w-full bg-white rounded-xl shadow-lg overflow-hidden">
                        <h2 className="text-xl font-semibold text-gray-800 px-6 pt-4 pb-2">Route Map</h2>
                        <img
                            loading="lazy"
                            src="/tempmap.png"
                            alt="Waste Management Route Map"
                            className="object-cover w-full h-60 md:h-80 lg:h-[400px]"
                        />
                    </section>

                    {/* Buttons Section */}
                    <section className="flex flex-col sm:flex-row gap-4 w-full justify-center">
                        <button className="flex items-center justify-center w-full sm:w-[150px] px-4 py-3 bg-emerald-600 text-white rounded-full font-semibold shadow-md hover:bg-emerald-700 transition duration-150">
                            Update Route
                        </button>
                        <button className="flex items-center justify-center w-full sm:w-[180px] px-4 py-3 bg-lime-100 text-stone-900 rounded-full font-semibold shadow-md hover:bg-lime-200 transition duration-150">
                            Send Route to Phone
                        </button>
                    </section>
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default DashboardPage;
