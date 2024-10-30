"use client";

import React from 'react';
import { useRouter } from 'next/navigation';

function InfoCard({ title, description, link }) {
    const router = useRouter();

    const handleMoreInfoClick = () => {
        if (link) {
            router.push(link);
        }
    };

    return (
        <section className="flex flex-col justify-center p-4 w-full max-w-[960px] min-h-[122px] max-md:max-w-full">
            <div className="flex flex-wrap gap-10 justify-between items-center px-5 py-5 w-full bg-white rounded-xl border border-solid border-stone-300 max-w-[928px] min-h-[90px] max-md:max-w-full">
                <div className="flex flex-col self-stretch my-auto text-base min-h-[48px] min-w-[240px] w-[619px] max-md:max-w-full">
                    <h2 className="flex flex-col max-w-full font-bold leading-none min-h-[20px] text-stone-900 w-[619px]">
                        {title}
                    </h2>
                    <p className="flex flex-col mt-1 max-w-full min-h-[24px] text-stone-500 w-[619px]">
                        {description}
                    </p>
                </div>
                <button
                    onClick={handleMoreInfoClick}
                    className="flex items-start self-stretch my-auto text-sm font-medium text-white min-h-[32px] w-[95px]">
                    <span className="flex overflow-hidden justify-center items-center px-4 bg-emerald-600 rounded-2xl min-h-[32px] w-[95px]">
                        More Info
                    </span>
                </button>
            </div>
        </section>
    );
}

export default InfoCard;