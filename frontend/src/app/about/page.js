import React from 'react';
import Header from '../../components/header';
import Footer from '../../components/footer';
import Link from 'next/link';

function AboutPage() {
    return (
        <div className="flex flex-col min-h-screen bg-gray-50 text-gray-900">
            <Header />

            {/* Hero Section */}
            <main className="flex flex-col items-center px-6 py-16 bg-white shadow-md">
                <h1 className="text-4xl font-bold text-gray-800 text-center mb-4">
                    About Waste Management Solutions
                </h1>
                <p className="text-lg text-gray-600 text-center max-w-3xl mb-6">
                    Waste Management Solutions is dedicated to helping cities, organizations, and communities manage waste efficiently and sustainably. Our platform offers powerful tools for route optimization, emission tracking, and insightful data analytics to make waste management smarter and eco-friendly.
                </p>
                <Link href="/register" className="px-6 py-3 bg-emerald-600 text-white rounded-full font-semibold hover:bg-emerald-700 transition duration-200">
                    Get Started
                </Link>
            </main>

            {/* Features Section */}
            <section className="flex flex-col items-center px-6 py-16 bg-gray-100">
                <h2 className="text-3xl font-bold text-gray-800 mb-8">Our Features</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl">
                    {/* Feature 1 */}
                    <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
                        <img src="/feature-route.svg" alt="Route Optimization" className="w-16 h-16 mb-4" />
                        <h3 className="text-xl font-semibold text-gray-700">Route Optimization</h3>
                        <p className="text-gray-600 mt-2 text-center">
                            Plan the most efficient routes to reduce travel distance, saving time and fuel, and reducing operational costs.
                        </p>
                    </div>

                    {/* Feature 2 */}
                    <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
                        <img src="/feature-emission.svg" alt="Emission Tracking" className="w-16 h-16 mb-4" />
                        <h3 className="text-xl font-semibold text-gray-700">Emission Tracking</h3>
                        <p className="text-gray-600 mt-2 text-center">
                            Monitor and manage emissions to make eco-friendly choices that reduce your carbon footprint and improve sustainability.
                        </p>
                    </div>

                    {/* Feature 3 */}
                    <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
                        <img src="/feature-data.svg" alt="Data Insights" className="w-16 h-16 mb-4" />
                        <h3 className="text-xl font-semibold text-gray-700">Data Insights</h3>
                        <p className="text-gray-600 mt-2 text-center">
                            Get actionable insights with detailed reports and analytics, helping you make data-driven decisions to improve waste management.
                        </p>
                    </div>
                </div>
            </section>

            {/* Mission Section */}
            <section className="flex flex-col items-center px-6 py-16 bg-white shadow-md">
                <h2 className="text-3xl font-bold text-gray-800 mb-4">Our Mission</h2>
                <p className="text-lg text-gray-600 max-w-2xl text-center mb-6">
                    At Waste Management Solutions, our mission is to promote sustainable waste management practices. We aim to reduce environmental impact by providing advanced tools that help you manage waste efficiently, reduce emissions, and support a cleaner, greener planet.
                </p>
                <Link href="/register" className="px-6 py-3 bg-emerald-600 text-white rounded-full font-semibold hover:bg-emerald-700 transition duration-200">
                    Join Us
                </Link>
            </section>

            {/* Call-to-Action Section */}
            <section className="flex flex-col items-center px-6 py-10 bg-gray-100">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4 text-center">Ready to Make a Difference?</h2>
                <p className="text-gray-600 text-center max-w-xl mb-6">
                    Start managing waste efficiently and sustainably today. Whether you’re a city planner, organization, or community, our platform provides you with the tools you need to make an impact.
                </p>
                <Link href="/register" className="px-8 py-3 bg-emerald-600 text-white font-bold rounded-full hover:bg-emerald-700 transition duration-200">
                    Get Started
                </Link>
            </section>

            <Footer />
        </div>
    );
}

export default AboutPage;