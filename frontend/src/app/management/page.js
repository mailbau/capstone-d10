import React from 'react';
import Header from '../../components/header';
import InfoCard from '../../components/infocard';
import TpsTable from './tpsTable';
import Footer from '../../components/footer';
import WithAuth from '@/components/withAuth';

function Management() {
    return (
        <div className="flex flex-col min-h-screen bg-gray-50">
            <Header />
            <main className="flex flex-col items-center w-full px-4 md:px-10 py-5">
                <div className="w-full max-w-5xl space-y-6">
                    {/* Centered Info Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
