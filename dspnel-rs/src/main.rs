use egg::{*, rewrite as rw};

define_language! {
    enum SimpleLanguage {
        "true" = True,
        "false" = False,

        "assign" = Assignment([Id; 2]),
        "add-assign" = AddAssignment([Id; 2]),
        "mul-assign" = MulAssignment([Id; 2]),
        "sub-assign" = SubAssignment([Id; 2]),

        "+" = Add([Id; 2]),
        "-" = Sub([Id; 2]),
        "/" = Div([Id; 2]),
        "*" = Mul([Id; 2]),
        "%" = Modulo([Id; 2]),
        "unary-minus" = UnaryMinus([Id; 1]),

        "and" = And([Id; 2]),
        "or" = Or([Id; 2]),
        "xor" = Xor([Id; 2]),
        "==>" = Imply([Id; 2]),
        "not" = Not([Id; 1]),

        ">" = GreaterThan([Id; 2]),
        ">=" = GreaterEquals([Id; 2]),
        "<" = LessThan([Id; 2]),
        "<=" = LessEquals([Id; 2]),
        "==" = Equality([Id; 2]),
        "!=" = Different([Id; 2]),

        "|" = BitwiseOr([Id; 2]),
        "&" = BitwiseAnd([Id; 2]),
        "<<" = BitshiftLeft([Id; 2]),
        ">>" = BitshiftRight([Id; 2]),
        "~" = BitNegation([Id; 1]),

        "prime" = Prime([Id; 1]),

        "call" = MethodCall(Vec<Id>),
        "get-attr" = GetAttribute([Id; 2]),

        "cond" = ConditionalExpression(Vec<Id>),

        "block" = Block(Vec<Id>),

        "return" = Return([Id; 1]),

        Integer(i64),
        Identifier(Symbol),
    }
}


fn main() {
    println!("Hello, world!");

    let rules: &[Rewrite<SymbolLang, ()>] = &[        
        rw!("commute-add"; "(+ ?x ?y)" => "(+ ?y ?x)"),
        rw!("commute-mul"; "(* ?x ?y)" => "(* ?y ?x)"),

        rw!("add-0"; "(+ ?x 0)" => "?x"),
        rw!("mul-0"; "(* ?x 0)" => "0"),
        rw!("mul-1"; "(* ?x 1)" => "?x"),
        rw!("div-one"; "?x" => "(/ ?x 1)"),

        rw!("mul-2-shift";
            "(* ?x 2)" => "(<< ?x 2)"
             //if is_integer_type("?x")
        ),

        rw!("not-true"; "(not true)" => "false"),
        rw!("not-false"; "(not false)" => "true"),
        rw!("not-not"; "(not (not ?x))" => "?x"),
        rw!("gt-eq-same"; "(>= ?x ?x)" => "true"),
        rw!("lt-eq-same"; "(<= ?x ?x)" => "true"),
        rw!("gt-same"; "(> ?x ?x)" => "false"),
        rw!("lt-same"; "(< ?x ?x)" => "false"),
        rw!("eq-same"; "(== ?x ?x)" => "true"),

        rw!("cancel-denominator"; "(* (/ ?a ?b) ?b)" => "?a"),
    ];

    let start: RecExpr<SymbolLang> = "(not (not (not (>= (+ 0 (* 1 a)) a))))".parse().unwrap();
    println!("{:?}", start.to_string());

    let runner = Runner::default().with_expr(&start).run(rules);

    let extractor = Extractor::new(&runner.egraph, AstSize);

    let (_best_cost, best_expr) = extractor.find_best(runner.roots[0]);

    println!("{:?}", best_expr.to_string());
}
