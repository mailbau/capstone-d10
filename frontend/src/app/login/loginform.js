import React from 'react';

function LoginForm() {
    return (
        <div className="flex justify-center items-center min-h-screen ">
            <div className="flex flex-col pt-5 pb-32 min-h-[632px] min-w-[240px] w-[512px] bg-white rounded-xl max-md:pb-24"> {/* Add shadow and rounded corners */}
                <h2 className="flex flex-col justify-center items-start p-4 w-full text-3xl font-bold tracking-tighter leading-none text-black whitespace-nowrap">
                    Login
                </h2>
                <form>
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
                            Login
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default LoginForm;
