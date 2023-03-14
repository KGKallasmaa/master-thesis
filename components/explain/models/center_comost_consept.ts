module CenterMostConsept {
  export interface Example {
    distanceToCenter: number;
    src: string;
  }

  export interface Concept {
    examples: Example[];
    name: string;
  }

  export interface CenterConsept {
    concepts: Concept[];
    label: string;
  }
}
export default CenterMostConsept;
