//Utility function to replace - with space and capitalize
export function capitalizedWord(str: string) {
  if (str === "ecommerce") return "Catégories";
  return str.replace(/-|\b\w/g, (match) => {
    if (match === "-") {
      return " ";
    }
    return match.toUpperCase();
  });
}
