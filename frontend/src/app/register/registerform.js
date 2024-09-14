import React from 'react';
import Link from 'next/link';

function RegisterForm() {
    return (
        <div className="flex justify-center items-center min-h-screen">
            <div className="flex flex-col pt-5 pb-32 min-h-[632px] min-w-[240px] w-[512px] bg-white rounded-xl max-md:pb-24"> {/* Add shadow and rounded corners */}
                <h2 className="flex flex-col justify-center items-start p-4 w-full text-3xl font-bold tracking-tighter leading-none text-black whitespace-nowrap">
                    Register
                </h2>
                <form>
                    <div className="flex flex-col px-4 py-3 w-full text-base">
                        <label htmlFor="firstName" className="pb-2 w-full font-medium text-stone-900">
                            First Name
                        </label>
                        <input
                            type="text"
                            id="firstName"
                            className="p-4 bg-lime-50 rounded-xl w-full min-h-[56px]"
                            placeholder="Enter your first name"
                        />
                    </div>

                    <div className="flex flex-col px-4 py-3 w-full text-base">
                        <label htmlFor="lastName" className="pb-2 w-full font-medium text-stone-900">
                            Last Name
                        </label>
                        <input
                            type="text"
                            id="lastName"
                            className="p-4 bg-lime-50 rounded-xl w-full min-h-[56px]"
                            placeholder="Enter your last name"
                        />
                    </div>

                    <div className="flex flex-col px-4 py-3 w-full text-base">
                        <label htmlFor="email" className="pb-2 w-full font-medium text-stone-900">
                            Email
                        </label>
                        <input
                            type="email"
                            id="email"
                            className="p-4 bg-lime-50 rounded-xl w-full min-h-[56px]"
                            placeholder="Enter your email"
                        />
                    </div>

                    <div className="flex flex-col px-4 py-3 w-full text-base">
                        <label htmlFor="password" className="pb-2 w-full font-medium text-stone-900">
                            Password
                        </label>
                        <input
                            type="password"
                            id="password"
                            className="p-4 bg-lime-50 rounded-xl w-full min-h-[56px]"
                            placeholder="Enter your password"
                        />
                    </div>

                    <div className="px-4 py-3 w-full">
                        <button
                            type="submit"
                            className="w-full px-5 py-3 bg-emerald-600 text-white font-bold rounded-3xl"
                        >
                            Register
                        </button>
                    </div>
                </form>
                <div className="flex justify-center items-center w-full py-4">
                    <p className="text-base text-gray-600">
                        Already have an account?{' '}
                        <Link href="/login" className="text-blue-600 font-bold hover:underline">
                            Login
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default RegisterForm;
