"use client"

import { createContext, useState } from "react";

export const InfoContext = createContext();

export default function InfoProvider({ children }){
    const [info, setInfo] = useState({});

    function handleInfo(title, text, id){
        setInfo({
            title: title, 
            text: text, 
            id: id
        });
    }

    return(
            <InfoContext.Provider value={{handleInfo, info}}>
                { children }
            </InfoContext.Provider>
    );
}
