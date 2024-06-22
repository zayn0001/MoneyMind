"use client"

import * as React from "react"
import Link from "next/link"
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
  NavigationMenuLink
} from "@/components/ui/navigation-menu"

import { navigationMenuTriggerStyle } from "@/components/ui/navigation-menu"
import Image from "next/image"

export default function NavBar() {
  return (
    <nav className="max-w-7xl flex mx-auto px-2 sm:px-6 lg:px-8 flex justify-between">
      <div className="relative flex flex-row items-center justify-between h-16">
      <NavigationMenu>
        <NavigationMenuList>
          <NavigationMenuItem>
            <Link href="/general">
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                General
              </NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <Link href="/portfolio">
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                Portfolio
              </NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
      </div>
      <div className="relative flex flex-row items-center justify-between h-16">
      <NavigationMenu>
        <NavigationMenuList>
          <NavigationMenuItem>
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
            <span className="mr-10">John Doe</span>
            <Image
                src="https://t3.ftcdn.net/jpg/02/18/23/02/360_F_218230230_OdCO2XyeMsH3ica7Um99uIeMnTFGyibC.jpg"
                alt="Profile Image"
                width={40}
                height={40}
                className="rounded-full"
              />
            </NavigationMenuLink>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
      </div>
    </nav>
  )
}
