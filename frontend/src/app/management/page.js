import React from 'react';
import Header from '../../components/header';
import InfoCard from '../../components/infocard';
import TpsTable from './tpsTable';
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
                    {/* Table */}
                    <TpsTable />
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default DashboardPage;