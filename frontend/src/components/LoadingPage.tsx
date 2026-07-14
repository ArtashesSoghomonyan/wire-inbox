import styles from "./LoadingPage.module.scss";

export default function LoadingPage() {
  return <div className={styles.center}>
    <div className={styles.loader}></div>
  </div>
}
