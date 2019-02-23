import pandas as pd
import argparse
from itertools import combinations_with_replacement
import sqlalchemy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Path to a json file {GeoID: qtid}', required=True)
    parser.add_argument('-t', '--table', help='Output table in database', required=False)
    parser.add_argument('-z', '--zoom', help='Zoom level', required=True)
    parser.add_argument('-c', '--conn', help='Database', required=False)

    args = parser.parse_args()
    file = args.input
    zoom = int(args.zoom)
    conn = args.conn
    table = args.table

    print("Input File: {}".format(file))

    data = pd.read_json(file, dtype={'geoid': str})

    print("Input Length: {}".format(len(data)))

    data2 = data.copy()
    data2.index = data2['geoid']
    data2 = data2.qtid.apply(pd.Series).stack().reset_index(level=1, drop=True)
    data2 = pd.DataFrame(data2, columns=['qtid']).reset_index()
    data2['z_qtid'] = data2.qtid.apply(lambda x: len(x))
    data2['n_qtid'] = data2['z_qtid'].apply(lambda x: 4**(zoom-x))

    geo_size = data2.groupby('geoid').apply(lambda x: sum(x.n_qtid))
    geo_size = pd.DataFrame(geo_size, columns=['n_qtid'])
    geo_size = geo_size.reset_index()

    data2 = pd.merge(data2.drop(['n_qtid'], axis=1), geo_size, on='geoid')
    sort_data = sorted(data2.values.tolist(), key=lambda x: (-x[2], x[3]))

    def fill_qt(qt, n=zoom):
        n_left = n - len(qt)
        return [qt + ''.join(c) for c in combinations_with_replacement('0123', n_left)]

    output = {}
    for s in sort_data:
        qt = s[1]
        gid = s[0]
        z_qt = s[2]
        if z_qt == zoom:
            output[qt] = output.get(qt, gid)
        else:
            qt_list = fill_qt(qt)
            for q in qt_list:
                output[q] = output.get(q, gid)

    output = pd.DataFrame.from_dict(output, orient='index', columns=['geoid'])
    output = output.reset_index().rename(columns={'index': 'qtid'})

    # write out
    output.to_csv('/opt/received_data/qtid_geoid.csv', index=False)
    data.to_csv('/opt/received_data/geoid_qtid.csv', index=False)

    if conn and table:
        print("Database Connection: {}".format(conn))
        print("Database Table: {}".format(table))
        engine = sqlalchemy.create_engine(conn)
        outtable1 = '{}_1'.format(table)
        outtable2 = '{}_2'.format(table)
        data.to_sql(outtable1, con=engine, if_exists='replace')
        print('(geoid: qtid) written to table {}'.format(outtable1))
        output.to_sql(outtable2, con=engine, if_exists='replace')
        print('(qtid: geoid) written to table {}'.format(outtable2))
