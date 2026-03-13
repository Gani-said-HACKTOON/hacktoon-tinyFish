"use client"
import { defaultOverrides } from "next/dist/server/require-hook"
import Link from "next/link"
import  Style  from "./navbar.module.css"
import { useState } from "react"

export default function Navbar(){
    const [open, setOpen] = useState(false)
    return(
        <nav className={Style.nav}>
            <div className={Style.container}>
                <h1>Dreelio</h1>
                <button onClick={() => setOpen(!open)}>☰</button>

            </div>
                            { open &&(
                    <div className={Style.menu}>
                        <a href="/">Features</a>
                        <a href="/">Benefit</a>
                        <a href="/">Pricing</a>
                        <a href="/">blog</a>
                        <a href="/">contact us</a>
                    </div>
                )

                }
        </nav>
    )
}