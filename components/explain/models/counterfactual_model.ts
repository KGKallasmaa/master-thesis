export interface CounterfactualExplanation {
  counterFactualClass: string;
  counterfactuals: CounterfactualInstance[];
  error: string;
  original: Original;
}

export interface CounterfactualInstance {
  dif: Map<string, number>;
  values: Map<string, number>;
}

export interface Original {
  class: number;
  values: Map<string, number>;
}
