import React from "react";
import Header from "../../components/header";
import Footer from "../../components/footer";

function TotalDistancePage() {
    return (
        <div className="flex overflow-hidden flex-col bg-white">
            <Header />
            <main className="flex justify-center items-start px-40 py-5 w-full min-h-[931px] max-md:px-5 max-md:max-w-full">
                <div className="flex flex-col min-h-[891px] min-w-[240px] w-full max-md:max-w-full"> {/* Adjusted width */}

                </div>
            </main>
            <Footer />
        </div>
    );
}

export default TotalDistancePage;
