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
import SignOutButton from "./SignOutButton"

export default function NavBar({user}) {
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
            <span className="mr-10">{user["displayName"]}</span>
            <Image
                src={user["photoURL"]}
                alt="Profile Image"
                width={40}
                height={40}
                className="rounded-full"
              />
              <SignOutButton></SignOutButton>
            </NavigationMenuLink>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
      </div>
    </nav>
  )
}
