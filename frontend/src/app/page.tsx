"use client";

import Typewriter from "typewriter-effect";

import styles from "./page.module.scss";


export default function Home() {
  return <div className={styles.center}>
    <div className={styles.logo}>Wire Inbox</div>
    <div className={styles.typewriter}>
      <Typewriter options={{
        strings: ["Private Chats", "Group Chats", "Anonymous Conversations With Filters", "Rooms"],
        autoStart: true,
        loop: true,
        cursor: "|",
      }} />
    </div>
    <div className={styles.container}>

    </div>
  </div>
}
