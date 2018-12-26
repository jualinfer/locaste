
export class Voting {
    id: string;
    name: string;
    desc: string;
    question: Question;
    start_date: string;
    end_date: string;
    pub_key: string;
    auths: Author[];
    tally: string;
    postproc: string;
    custom_url: string;
}

export class Question {
    desc: string;
    options: Option[];
}

export class Author {
    name: string;
    url: string;
    me: boolean;
}

export class Option{
    number: number;
    option: string;
}