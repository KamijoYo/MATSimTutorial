package org.matsim.project;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

import org.matsim.api.core.v01.Coord;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.TransportMode;
import org.matsim.api.core.v01.network.Link;
import org.matsim.api.core.v01.network.Network;
import org.matsim.contrib.dvrp.fleet.DvrpVehicle;
import org.matsim.contrib.dvrp.fleet.DvrpVehicleImpl;
import org.matsim.contrib.dvrp.fleet.DvrpVehicleSpecification;
import org.matsim.contrib.dvrp.fleet.FleetWriter;
import org.matsim.contrib.dvrp.fleet.ImmutableDvrpVehicleSpecification;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.gbl.MatsimRandom;
import org.matsim.core.network.NetworkUtils;
import org.matsim.core.network.io.MatsimNetworkReader;
import org.matsim.core.scenario.ScenarioUtils;

import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvValidationException;

/**
 * @author  Yo Kamijo
 * This is an example script to create taxi vehicle files. 
 *
 */

public class RunCreateDrtMesh {
	
	public static void addVehicles(List<DvrpVehicleSpecification> vehicles, int count, Link link, int size, int seats1, double operationStartTime, double operationEndTime) {
        for (int i = 0; i < size; i++) {
            vehicles.add(ImmutableDvrpVehicleSpecification.newBuilder()
                    .id(Id.create("drt" + count, DvrpVehicle.class))
                    .startLinkId(link.getId())
                    .capacity(seats1)
                    .serviceBeginTime(operationStartTime)
                    .serviceEndTime(operationEndTime)
                    .build());
            count += 1;
        }
    }
	public static void main(String[] args) throws CsvValidationException {
		Scenario scenario = ScenarioUtils.createScenario(ConfigUtils.createConfig());
		double operationStartTime = 0.;
		double operationEndTime = 32*3600.;
		int seats = 4;
		int size = 1;
		int count = 0;
		String networkfile = "scenarios/equil/manhattan.xml";
		List<List<String>> records = new ArrayList<List<String>>();
		try (CSVReader csvReader = new CSVReader(new FileReader("scenarios/equil/NYCHex0.csv"));) {
		    String[] values = null;
		    while ((values = csvReader.readNext()) != null) {
		        records.add(Arrays.asList(values));
		    }
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		//ヘッダーを消すコマンド（ヘッダーも読み込まれていくため）
		records.remove(0);
		System.out.println(records);
		List<DvrpVehicleSpecification> vehicles = new ArrayList<>();
		new MatsimNetworkReader(scenario.getNetwork()).readFile(networkfile);
		Network network = scenario.getNetwork();
		for(List<String> row: records) {
			Coord coord = new Coord(Double.parseDouble(row.get(2)),Double.parseDouble(row.get(3)));
			Link startLink;
			startLink = NetworkUtils.getNearestLink(network, coord);
			addVehicles(vehicles, count, startLink, size, seats, operationStartTime, operationEndTime);
            count += size;
		}
		String drtsFile = "scenarios/equil/drts"+count + "S" + seats +".xml";
		System.out.println(drtsFile);
		new FleetWriter(vehicles.stream()).write(drtsFile);
	}

}
