import React from 'react';

function TpsTable() {
    const garbageBins = [
        { id: 'Bin001', location: '123 Main St', capacity: '1000lb', lastEmptied: '2023-10-01' },
        { id: 'Bin002', location: '456 Elm St', capacity: '800lb', lastEmptied: '2023-10-02' },
        { id: 'Bin003', location: '789 Oak St', capacity: '1200lb', lastEmptied: '2023-10-03' },
        { id: 'Bin004', location: '101 Pine St', capacity: '600lb', lastEmptied: '2023-10-04' },
        { id: 'Bin005', location: '202 Maple St', capacity: '1500lb', lastEmptied: '2023-10-05' },
    ];

    return (
        <section className="flex flex-col justify-center px-4 py-3 w-full text-sm min-h-[432px]">
            <div className="flex overflow-hidden flex-col w-full bg-white rounded-xl border border-solid border-stone-300 min-h-[408px]">
                <div className="flex flex-col w-full min-h-[406px]">
                    <header className="flex flex-col w-full font-medium max-w-[926px] min-h-[46px] text-stone-900 max-md:max-w-full">
                        <div className="flex flex-wrap items-start w-full bg-white min-h-[46px]">
                            <div className="flex flex-col grow shrink justify-center px-4 py-3.5 min-h-[46px] w-[171px]">
                                <span className="max-w-full min-h-[21px] w-[166px]">Garbage Bin ID</span>
                            </div>
                            <div className="flex flex-col grow shrink justify-center px-4 py-3.5 whitespace-nowrap min-h-[46px] w-[170px]">
                                <span className="max-w-full min-h-[21px] w-[165px]">Location</span>
                            </div>
                            <div className="flex flex-col grow shrink justify-center px-4 py-3.5 whitespace-nowrap min-h-[46px] w-[171px]">
                                <span className="max-w-full min-h-[21px] w-[167px]">Capacity</span>
                            </div>
                            <div className="flex flex-col grow shrink justify-center px-4 py-3.5 min-h-[46px] w-[169px]">
                                <span className="max-w-full min-h-[21px] w-[164px]">Last Emptied</span>
                            </div>
                            <div className="flex flex-col grow shrink justify-center px-4 py-3.5 whitespace-nowrap min-h-[46px] w-[110px]">
                                <span className="max-w-full min-h-[21px] w-[105px]">Actions</span>
                            </div>
                        </div>
                    </header>
                    <div className="flex flex-col w-full max-w-[926px] min-h-[360px] text-stone-500 max-md:max-w-full">
                        {garbageBins.map((bin, index) => (
                            <div key={bin.id} className="flex flex-wrap items-start w-full border-t border-gray-200 min-h-[72px]">
                                <div className="flex flex-col grow shrink justify-center items-center px-4 py-7 whitespace-nowrap min-h-[72px] text-stone-900 w-[171px]">
                                    <span className="max-w-full min-h-[21px] w-[166px]">{bin.id}</span>
                                </div>
                                <div className="flex flex-col grow shrink justify-center items-center px-4 py-7 min-h-[72px] w-[170px]">
                                    <span className="max-w-full min-h-[21px] w-[165px]">{bin.location}</span>
                                </div>
                                <div className="flex flex-col grow shrink justify-center items-center px-4 py-7 whitespace-nowrap min-h-[72px] w-[171px]">
                                    <span className="max-w-full min-h-[21px] w-[167px]">{bin.capacity}</span>
                                </div>
                                <div className="flex flex-col grow shrink justify-center items-center px-4 py-7 whitespace-nowrap min-h-[72px] w-[169px]">
                                    <span className="max-w-full min-h-[21px] w-[164px]">{bin.lastEmptied}</span>
                                </div>
                                <div className="flex flex-col grow shrink justify-center items-center px-4 py-7 font-bold tracking-wide whitespace-nowrap min-h-[72px] w-[110px]">
                                    <button className="max-w-full min-h-[21px] w-[105px]">Edit</button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}

export default TpsTable;