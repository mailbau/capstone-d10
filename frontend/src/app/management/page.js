import React from 'react';
import Header from '../../components/header';
import InfoCard from '../../components/infocard';
import TpsTable from './tpsTable';
import Footer from '../../components/footer';

function Management() {
    return (
        <div className="flex overflow-hidden flex-col bg-white">
            <Header />
            <main className="flex justify-center items-start px-40 py-5 w-full min-h-[931px] max-md:px-5 max-md:max-w-full">
                <div className="flex flex-col min-h-[891px] min-w-[240px] w-full max-md:max-w-full"> {/* Adjusted width */}
                    {/* Centered Info Cards */}
                    <div className="flex flex-col items-center mb-4"> {/* Added flex container for centering */}
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
                    </div>
                    {/* Table */}
                    <TpsTable />
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default Management;