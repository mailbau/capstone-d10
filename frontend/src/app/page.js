import Link from 'next/link';
import React from 'react';
import Header from '@/components/header';
import Footer from '@/components/footer';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-between min-h-screen bg-gray-50 text-gray-900">
      {/* Header Section */}
      <header className="flex items-center justify-between w-full px-10 py-6 bg-white shadow-md">
        <div className="flex items-center gap-3">
          <img loading="lazy" src="/logo.svg" alt="logo" className="w-8 h-8" />
          <h1 className="text-2xl font-semibold text-stone-900">
            Capstone D-10
          </h1>
        </div>
        <nav>
          <Link href="/login" className="px-5 py-2 text-white bg-emerald-600 rounded-full hover:bg-emerald-700 transition duration-200">
            Login
          </Link>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="flex flex-col items-center w-full px-6 py-12 text-center">
        <h1 className="text-5xl font-extrabold text-gray-900 leading-tight">
          Manage Waste Efficiently
        </h1>
        <p className="text-lg text-gray-600 mt-4 max-w-xl">
          Your one-stop solution for effective and sustainable waste management. Track routes, reduce emissions, and make a positive impact on the environment.
        </p>
        <div className="mt-8 flex gap-4">
          <Link href="/register" className="px-6 py-3 bg-emerald-600 text-white rounded-full font-semibold hover:bg-emerald-700 transition duration-200">
            Get Started
          </Link>
          <Link href="/about" className="px-6 py-3 bg-gray-100 text-gray-800 rounded-full font-semibold hover:bg-gray-200 transition duration-200">
            Learn More
          </Link>
        </div>
      </main>

      {/* Feature Highlights Section */}
      <section className="flex flex-col items-center w-full px-6 py-12 bg-gray-100">
        <h2 className="text-3xl font-bold text-gray-800 mb-8">Why Choose Us?</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl">
          <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
            <img src="/map.jpg" alt="Route Optimization" className="w-30 h-16 mb-4" />
            <h3 className="text-xl font-semibold text-gray-700">Route Optimization</h3>
            <p className="text-gray-600 mt-2 text-center">
              Plan the most efficient routes to reduce travel distance, saving time and fuel.
            </p>
          </div>
          <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
            <img src="/emission.png" alt="Emission Tracking" className="w-30 h-16 mb-4" />
            <h3 className="text-xl font-semibold text-gray-700">Emission Tracking</h3>
            <p className="text-gray-600 mt-2 text-center">
              Monitor emissions and make eco-friendly choices to reduce your carbon footprint.
            </p>
          </div>
          <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
            <img src="/data.jpg" alt="Data Insights" className="w-18 h-16 mb-4" />
            <h3 className="text-xl font-semibold text-gray-700">Data Insights</h3>
            <p className="text-gray-600 mt-2 text-center">
              Get actionable insights with detailed reports to improve waste management strategies.
            </p>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <Footer />
    </div>
  );
}
