import os
import csv

FLAGS = _ = None
DEBUG = False


def read_members(path):
    data = list()
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row['StudentNumber'])
    data.sort()
    return data


def read_score(path):
    data = dict()
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        pnames = reader.fieldnames[1:]
        for row in reader:
            sn = row['StudentNumber']
            score = list()
            for p in pnames:
                score.append(int(row[p]))
            data[sn] = score
    return data


def read_deadline(path):
    data = list()
    base = list()
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        magnitude = list(map(float, reader.fieldnames[1:]))
        magnitude.sort(reverse=True)
        for row in reader:
            d = dict()
            for mag in magnitude:
                key = int(row[str(mag)])
                d[key] = mag
            data.append(d)
            base.append(float(row['base']))
    return base, data


def calc(score, base, deadline):
    result = list()
    for s, b, d in zip(score, base, deadline):
        if s < 0:
            result.append('')
            continue
        if s > max(d.keys()):
            result.append('')
            continue
        for k, v in sorted(d.items()):
            if s <= k:
                result.append(f'={b}*{v}')
                break
    return result


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    members = read_members(FLAGS.members)
    if DEBUG:
        print(members)

    score = read_score(FLAGS.score)
    if DEBUG:
        print(score)

    base, deadline = read_deadline(FLAGS.deadline)
    if DEBUG:
        print(base)
        print(deadline)

    with open(FLAGS.output, 'w') as f:
        writer = csv.DictWriter(
            f, fieldnames=['StudentNumber'] + base,
            quoting=csv.QUOTE_MINIMAL, lineterminator=os.linesep)
        writer.writeheader()
        for m in members:
            if m in score.keys():
                s = score[m]
            else:
                s = [-1]*len(base)
            data = calc(s, base, deadline)
            entry = dict()
            entry['StudentNumber'] = m
            for i, b in enumerate(base):
                entry[b] = data[i]
            writer.writerow(entry)


if __name__ == '__main__':
    root_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(root_path)
    os.chdir(root_dir)

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true',
                        help='On or off debug message')
    parser.add_argument('--members', type=str, required=True,
                        help='The member csv path')
    parser.add_argument('--score', type=str, required=True,
                        help='The exported score path from domjudge')
    parser.add_argument('--deadline', type=str, required=True,
                        help='The deadline csv paht')
    parser.add_argument('--output', type=str, default='output.csv',
                        help='The output path')

    FLAGS, _ = parser.parse_known_args()

    FLAGS.members = os.path.abspath(os.path.expanduser(FLAGS.members))
    FLAGS.score = os.path.abspath(os.path.expanduser(FLAGS.score))
    FLAGS.deadline = os.path.abspath(os.path.expanduser(FLAGS.deadline))
    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))

    DEBUG = FLAGS.debug

    main()

